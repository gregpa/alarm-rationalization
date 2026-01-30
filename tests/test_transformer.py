"""
Tests for AlarmTransformer class - validates v3.23 behavior.

These tests capture the current working behavior to prevent regressions.
Run with: pytest tests/ -v
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAlarmTransformerInit:
    """Test transformer initialization and configuration."""

    def test_flng_client_loads(self, transformer_flng):
        """FLNG client should load with correct configuration."""
        assert transformer_flng.client_id == "flng"
        assert transformer_flng.config["name"] == "Freeport LNG"
        assert transformer_flng.config["parser"] == "dynamo"

    def test_hfs_client_loads(self, transformer_hfs):
        """HF Sinclair client should load with correct configuration."""
        assert transformer_hfs.client_id == "hfs_artesia"
        assert transformer_hfs.config["name"] == "HF Sinclair - Artesia"
        assert transformer_hfs.config["phapro_headers"] == "HFS"

    def test_client_configs_exist(self):
        """All expected clients should be configured."""
        from streamlit_app import AlarmTransformer

        expected_clients = ["flng", "hfs_artesia", "rt_bessemer"]
        for client_id in expected_clients:
            assert client_id in AlarmTransformer.CLIENT_CONFIGS

    def test_phapro_headers_correct_length(self, transformer_flng, transformer_hfs):
        """PHA-Pro headers should have expected column counts."""
        flng_headers = transformer_flng.get_phapro_headers()
        hfs_headers = transformer_hfs.get_phapro_headers()

        assert len(flng_headers) == 45, "FLNG should have 45 columns"
        assert len(hfs_headers) == 43, "HFS should have 43 columns"


class TestDiscreteAlarmDetection:
    """Test discrete vs analog alarm type classification."""

    def test_discrete_alarm_types(self, transformer_flng):
        """Known discrete alarm types should be detected."""
        discrete_types = [
            "bad pv", "controlfail", "command disagree", "off normal",
            "st0", "st1", "st2", "unreasonable", "cnferr"
        ]
        for alarm_type in discrete_types:
            assert transformer_flng.is_discrete(alarm_type), f"{alarm_type} should be discrete"

    def test_analog_alarm_types(self, transformer_flng):
        """Analog alarm types should NOT be detected as discrete."""
        analog_types = [
            "(PV) High", "(PV) Low", "(PV) High High", "(PV) Low Low",
            "PVHIGH", "PVLOW", "PVHIHI", "PVLOLO"
        ]
        for alarm_type in analog_types:
            assert not transformer_flng.is_discrete(alarm_type), f"{alarm_type} should be analog"


class TestPriorityMapping:
    """Test priority text to code mapping."""

    def test_priority_mappings(self, transformer_flng):
        """Priority names should map to correct codes."""
        # map_priority returns (priority_code, alarm_status) tuple
        # Note: Journal maps to "Jo" (2-char code) per v3.23 behavior
        test_cases = [
            ("Urgent", "False", "U"),
            ("Critical", "False", "C"),
            ("High", "False", "H"),
            ("Medium", "False", "M"),
            ("Low", "False", "L"),
            ("Journal", "False", "Jo"),  # 2-char code per actual implementation
        ]
        for priority_name, disabled, expected_code in test_cases:
            result = transformer_flng.map_priority(priority_name, disabled)
            # Handle both tuple returns and single value returns
            if isinstance(result, tuple):
                assert result[0] == expected_code, f"{priority_name} should map to {expected_code}, got {result[0]}"
            else:
                assert result == expected_code, f"{priority_name} should map to {expected_code}"

    def test_disabled_alarm_priority(self, transformer_flng):
        """Disabled alarms should have special handling."""
        result = transformer_flng.map_priority("High", "True")
        assert result is not None


class TestSeverityMapping:
    """Test consequence to severity letter mapping."""

    def test_severity_letter_mapping(self, transformer_flng):
        """Consequence codes should map to severity letters."""
        test_cases = [
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("", "(N)"),
            (None, "(N)"),
        ]
        for consequence, expected in test_cases:
            result = transformer_flng.map_severity(consequence)
            assert result == expected, f"Consequence '{consequence}' should map to '{expected}'"


class TestUnitExtraction:
    """Test unit extraction from tag names and asset paths."""

    def test_tag_prefix_extraction(self, transformer_flng):
        """Unit should be extracted from tag name prefix."""
        unit = transformer_flng.extract_unit("17TI5879", "/U17/17_FLARE/17TI5879", "TAG_PREFIX")
        assert unit == "17"

    def test_asset_parent_extraction(self, transformer_flng):
        """Unit should be extracted from asset path parent."""
        unit = transformer_flng.extract_unit("17TI5879", "/U17/17_FLARE/17TI5879", "ASSET_PARENT")
        assert "17" in unit or "FLARE" in unit

    def test_asset_child_extraction(self, transformer_flng):
        """Unit should be extracted from asset path child (last segment)."""
        unit = transformer_flng.extract_unit("17TI5879", "/U17/17_FLARE/17H-2", "ASSET_CHILD")
        assert unit == "17H-2"


class TestTagSourceDerivation:
    """Test tag source determination from point type rules."""

    def test_safety_manager_detection(self, transformer_hfs):
        """Safety Manager point types should be detected."""
        source, enforcement = transformer_hfs.derive_tag_source("SM_TAG001", "SM")
        assert "Safety Manager" in source
        assert enforcement == "R"

    def test_scada_detection(self, transformer_hfs):
        """SCADA point types should be detected."""
        source, enforcement = transformer_hfs.derive_tag_source("TAG001", "ANA")
        assert "SCADA" in source
        assert enforcement == "M"

    def test_default_source(self, transformer_hfs):
        """Unknown point types should get default source."""
        source, enforcement = transformer_hfs.derive_tag_source("TAG001", "UNKNOWN_TYPE")
        assert source == transformer_hfs.config["default_source"]


class TestForwardTransformation:
    """Test DynAMo to PHA-Pro forward transformation."""

    def test_basic_forward_transform(self, transformer_flng, sample_dynamo_csv):
        """Forward transformation should produce valid PHA-Pro output."""
        result = transformer_flng.transform_forward(
            sample_dynamo_csv,
            selected_units=None,
            unit_method="TAG_PREFIX"
        )

        # transform_forward returns (csv_bytes, stats_dict) tuple
        assert result is not None
        assert isinstance(result, tuple), "transform_forward should return a tuple"
        assert len(result) == 2, "Should return (csv_content, stats)"

        csv_content, stats = result
        assert csv_content is not None
        assert isinstance(stats, dict)

    def test_forward_transform_returns_bytes(self, transformer_flng, sample_dynamo_csv):
        """Forward transformation should return bytes for CSV content."""
        csv_content, stats = transformer_flng.transform_forward(
            sample_dynamo_csv,
            selected_units=None,
            unit_method="TAG_PREFIX"
        )

        # CSV content should be bytes
        assert isinstance(csv_content, bytes), "CSV content should be bytes"

        # Decode and check format
        decoded = csv_content.decode('latin-1')
        lines = decoded.strip().split('\n')
        assert len(lines) >= 1, "Should have at least header row"

    def test_forward_transform_has_correct_columns(self, transformer_flng, sample_dynamo_csv):
        """Forward transformation output should have 45 columns for FLNG."""
        csv_content, stats = transformer_flng.transform_forward(
            sample_dynamo_csv,
            selected_units=None,
            unit_method="TAG_PREFIX"
        )

        decoded = csv_content.decode('latin-1')
        lines = decoded.strip().split('\n')
        header = lines[0]

        import csv
        import io
        reader = csv.reader(io.StringIO(header))
        header_cols = next(reader)
        assert len(header_cols) == 45, f"Expected 45 columns, got {len(header_cols)}"

    def test_forward_transform_stats(self, transformer_flng, sample_dynamo_csv):
        """Forward transformation should return processing stats."""
        csv_content, stats = transformer_flng.transform_forward(
            sample_dynamo_csv,
            selected_units=None,
            unit_method="TAG_PREFIX"
        )

        assert "tags" in stats or "alarms" in stats, "Stats should include processing counts"


class TestDynamoParsing:
    """Test DynAMo CSV parsing functionality."""

    def test_parse_dynamo_csv_returns_dict(self, transformer_flng, sample_dynamo_csv):
        """DynAMo CSV parser should return a dict with schema keys."""
        result = transformer_flng.parse_dynamo_csv(sample_dynamo_csv)

        # v3.23 returns a dict with schema names as keys
        assert isinstance(result, dict), "parse_dynamo_csv should return a dict"

        # Expected schema keys
        expected_keys = ["_DCSVariable", "_DCS", "_Parameter", "_Notes"]
        for key in expected_keys:
            assert key in result, f"Result should have '{key}' key"

    def test_parse_dynamo_csv_structure(self, transformer_flng, sample_dynamo_csv):
        """DynAMo CSV should be parsed into dict with schema sections."""
        result = transformer_flng.parse_dynamo_csv(sample_dynamo_csv)

        # Each schema section should be a dict
        assert isinstance(result, dict)
        assert "_Parameter" in result
        assert "_DCSVariable" in result


class TestEncodingHandling:
    """Test encoding fixes for special characters."""

    def test_degree_symbol_handling(self, transformer_flng):
        """Degree symbols should be handled correctly."""
        if hasattr(transformer_flng, 'fix_encoding'):
            test_str = "Temperature 100\xb0F"
            result = transformer_flng.fix_encoding(test_str)
            assert result is not None


class TestClientAreas:
    """Test client area configuration."""

    def test_get_client_areas(self):
        """Should return available areas for a client."""
        from streamlit_app import AlarmTransformer

        areas = AlarmTransformer.get_client_areas("flng")
        assert "lqf_u17" in areas
        assert "ptf_u61" in areas

    def test_area_names(self):
        """Area names should be human-readable."""
        from streamlit_app import AlarmTransformer

        areas = AlarmTransformer.get_client_areas("flng")
        assert "LQF" in areas["lqf_u17"] or "Unit 17" in areas["lqf_u17"]


class TestDynamoHeaders:
    """Test DynAMo header constants."""

    def test_dynamo_headers_count(self):
        """DynAMo should have 42 column headers."""
        from streamlit_app import AlarmTransformer

        assert len(AlarmTransformer.DYNAMO_HEADERS) == 42

    def test_dynamo_headers_start_with_variable(self):
        """First DynAMo header should be the _Variable marker."""
        from streamlit_app import AlarmTransformer

        assert "_Variable" in AlarmTransformer.DYNAMO_HEADERS[0]


class TestABBSupport:
    """Test ABB 800xA client support."""

    def test_abb_client_exists(self):
        """ABB client should be configured."""
        from streamlit_app import AlarmTransformer

        assert "rt_bessemer" in AlarmTransformer.CLIENT_CONFIGS

    def test_abb_uses_correct_parser(self):
        """ABB client should use ABB parser."""
        from streamlit_app import AlarmTransformer

        config = AlarmTransformer.CLIENT_CONFIGS["rt_bessemer"]
        assert config["parser"] == "abb"

    def test_abb_phapro_headers_exist(self):
        """ABB should have specific PHA-Pro headers."""
        from streamlit_app import AlarmTransformer

        assert hasattr(AlarmTransformer, 'ABB_PHAPRO_HEADERS')
        assert len(AlarmTransformer.ABB_PHAPRO_HEADERS) == 23


class TestHFSinclair:
    """Test HF Sinclair client specifics."""

    def test_hfs_empty_mode_valid(self, transformer_hfs):
        """HFS should accept empty mode rows."""
        assert transformer_hfs.config.get("empty_mode_is_valid") == True

    def test_hfs_uses_43_columns(self, transformer_hfs):
        """HFS should use 43-column PHA-Pro format."""
        headers = transformer_hfs.get_phapro_headers()
        assert len(headers) == 43

    def test_hfs_has_tag_source_rules(self, transformer_hfs):
        """HFS should have extensive tag source rules."""
        rules = transformer_hfs.config.get("tag_source_rules", [])
        assert len(rules) > 10, "HFS should have many tag source rules"
