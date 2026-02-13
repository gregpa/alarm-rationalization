"""
Pytest configuration and fixtures for alarm-rationalization tests.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import from streamlit_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_dynamo_csv():
    """Sample DynAMo CSV content for testing forward transformation."""
    return '''_DCSVariable,_DCS,_Parameter
"'_Variable","name","_Parameter","mode","boundary","alarmType","alarmName","value","enforcement","priorityName","priorityValue","priorityEnforcement","consequence","TimeToRespond","pre-Alarm","historyTag","Purpose of Alarm","Consequence of No Action","Board Operator","Field Operator","Supporting Notes","TypeParameter","TypeValue","TypeEnforcement","DisabledParameter","DisabledValue","DisabledEnforcement","SuppressedParameter","SuppressedValue","SuppressedEnforcement","OnDelayParameter","OnDelayValue","OnDelayEnforcement","OffDelayParameter","OffDelayValue","OffDelayEnforcement","DeadBandParameter","DeadBandValue","DeadBandEnforcement","DeadBandUnitParameter","DeadBandUnitValue","DeadBandUnitEnforcement"
"/U17/17_FLARE/17TI5879","17TI5879","PID","NORMAL","upper","(PV) High","PVHIGH","850","M","High","3","M","","","","","Monitor temperature","Potential overheat","Acknowledge alarm","Investigate","","PV","150","M","Disabled","False","M","Suppressed","False","M","OnDelay","0","M","OffDelay","0","M","DeadBand","5","M","DeadBandUnit","%","M"
"/U17/17_FLARE/17TI5879","17TI5879","PID","NORMAL","lower","(PV) Low","PVLOW","100","M","Medium","2","M","","","","","Monitor temperature","Potential freeze","Acknowledge alarm","Investigate","","PV","150","M","Disabled","False","M","Suppressed","False","M","OnDelay","0","M","OffDelay","0","M","DeadBand","5","M","DeadBandUnit","%","M"
"/U17/17_FLARE/17FI1234","17FI1234","REGCTL","NORMAL","upper","(PV) High High","PVHIHI","95","R","Urgent","4","R","A","5","","","Critical flow limit","Equipment damage","Trip system","Evacuate area","Safety critical","PV","50","M","Disabled","False","M","Suppressed","False","M","OnDelay","2","M","OffDelay","5","M","DeadBand","1","M","DeadBandUnit","EU","M"
'''


@pytest.fixture
def sample_dynamo_discrete_csv():
    """Sample DynAMo CSV with discrete alarm types."""
    return '''_DCSVariable,_DCS,_Parameter
"'_Variable","name","_Parameter","mode","boundary","alarmType","alarmName","value","enforcement","priorityName","priorityValue","priorityEnforcement","consequence","TimeToRespond","pre-Alarm","historyTag","Purpose of Alarm","Consequence of No Action","Board Operator","Field Operator","Supporting Notes","TypeParameter","TypeValue","TypeEnforcement","DisabledParameter","DisabledValue","DisabledEnforcement","SuppressedParameter","SuppressedValue","SuppressedEnforcement","OnDelayParameter","OnDelayValue","OnDelayEnforcement","OffDelayParameter","OffDelayValue","OffDelayEnforcement","DeadBandParameter","DeadBandValue","DeadBandEnforcement","DeadBandUnitParameter","DeadBandUnitValue","DeadBandUnitEnforcement"
"/U17/17_VALVES/17XV001","17XV001","DEVCTL","NORMAL","","Bad PV","BADPV","","M","High","3","M","","","","","Valve fault detection","Valve malfunction","Acknowledge","Check valve","","","","","Disabled","False","M","Suppressed","False","M","OnDelay","0","M","OffDelay","0","M","DeadBand","","M","DeadBandUnit","","M"
"/U17/17_VALVES/17XV001","17XV001","DEVCTL","NORMAL","","Command Disagree","CMDDIS","","M","Critical","4","M","B","10","","","Valve position mismatch","Incorrect position","Investigate","Check actuator","","","","","Disabled","False","M","Suppressed","False","M","OnDelay","5","M","OffDelay","0","M","DeadBand","","M","DeadBandUnit","","M"
'''


@pytest.fixture
def sample_phapro_csv():
    """Sample PHA-Pro CSV content for testing reverse transformation."""
    return '''Unit,Tag Name,Old Tag Description,New Tag Description,P&ID,Range Min,Range Max,Engineering Units,Tag Source,Rationalization (Tag) Comment,Old Tag Enable Status,New Tag Enable Status,Alarm Type,Old Individual Alarm Enable Status,New Individual Alarm Enable Status,Old (BPCS) Priority,New (BPCS) Priority,Old Limit,New Limit,Old Deadband,New Deadband,Old Deadband Units,New Deadband Units,Old On-Delay Time,New On-Delay Time,Old Off-Delay Time,New Off-Delay Time,Rationalization Status,Alarm Status,Rationalization (Alarm) Comment,Limit Owner,Alarm HAZOP Comment,Alarm Suppression Notes,Alarm Class,Cause(s),Consequence(s),Inside Action(s),Outside Action(s),Health and Safety,Environment,Financial,Reputation,Privilege to Operate,Max Severity,Allowable Time to Respond
17,17TI5879,Monitor temperature,Monitor temperature,P&ID-001,0,1000,DEG F,Honeywell TDC (DCS),,Enabled,Enabled,(PV) High,Enabled,Enabled,High,Critical,850,900,5,5,%,%,0,0,0,0,Rationalized,Active,,Operations,,,,High temp causes overheat,Equipment damage,Acknowledge and investigate,Check equipment,Yes,No,Yes,No,No,B,10
17,17TI5879,Monitor temperature,Monitor temperature,P&ID-001,0,1000,DEG F,Honeywell TDC (DCS),,Enabled,Enabled,(PV) Low,Enabled,Disabled,Medium,Low,100,50,5,5,%,%,0,0,0,0,Rationalized,Disabled,Not needed per review,Operations,,,,Low temp not critical,Minor impact,Monitor,None,No,No,No,No,No,E,60
'''


@pytest.fixture
def transformer_flng():
    """Create an AlarmTransformer instance for FLNG client."""
    # Import here to avoid issues with streamlit
    from streamlit_app import AlarmTransformer
    return AlarmTransformer("flng", "lqf_u17")


@pytest.fixture
def transformer_hfs():
    """Create an AlarmTransformer instance for HF Sinclair client."""
    from streamlit_app import AlarmTransformer
    return AlarmTransformer("hfs_artesia", "north_console")


@pytest.fixture
def transformer_petrostar():
    """Create an AlarmTransformer instance for Petrostar Valdez client."""
    from streamlit_app import AlarmTransformer
    return AlarmTransformer("petrostar_valdez", "10_cdu")


@pytest.fixture
def sample_deltav_xml():
    """Sample DeltaV SAMAlarmsReport XML for testing."""
    return b'''<?xml version="1.0" encoding="utf-8"?>
<SAMAlarmsReport>
  <Alarm>
    <AlarmSourceName>14-TI-1234</AlarmSourceName>
    <AlarmSourceDescription>DHT Reactor Inlet Temp</AlarmSourceDescription>
    <Attribute>HI_ALM</Attribute>
    <Enable>True</Enable>
    <Priority>WARNING</Priority>
    <LimitValue>750</LimitValue>
    <Hysteresis>5</Hysteresis>
    <OnDelay>0</OnDelay>
    <OffDelay>0</OffDelay>
    <Path>14_DHT/V-14203/CTRL_MOD/14-TI-1234/HI_ALM</Path>
    <Type>Analog</Type>
    <FunctionalClassificationName>Equipment Protection</FunctionalClassificationName>
  </Alarm>
  <Alarm>
    <AlarmSourceName>14-TI-1234</AlarmSourceName>
    <AlarmSourceDescription>DHT Reactor Inlet Temp</AlarmSourceDescription>
    <Attribute>HI_HI_ALM</Attribute>
    <Enable>True</Enable>
    <Priority>CRITICAL_N</Priority>
    <LimitValue>800</LimitValue>
    <Hysteresis>5</Hysteresis>
    <OnDelay>0</OnDelay>
    <OffDelay>0</OffDelay>
    <Path>14_DHT/V-14203/CTRL_MOD/14-TI-1234/HI_HI_ALM</Path>
    <Type>Analog</Type>
    <FunctionalClassificationName>Safety</FunctionalClassificationName>
  </Alarm>
  <Alarm>
    <AlarmSourceName>18-AI-6128</AlarmSourceName>
    <AlarmSourceDescription>H2 Purity Analyzer</AlarmSourceDescription>
    <Attribute>LO_ALM</Attribute>
    <Enable>True</Enable>
    <Priority>ADVISORY</Priority>
    <LimitValue>95.0</LimitValue>
    <Hysteresis>1</Hysteresis>
    <OnDelay>30</OnDelay>
    <OffDelay>0</OffDelay>
    <Path>18_H2/H2-UNIT/CTRL_MOD/18-AI-6128/LO_ALM</Path>
    <Type>Analog</Type>
    <FunctionalClassificationName>Process Efficiency</FunctionalClassificationName>
  </Alarm>
  <Alarm>
    <AlarmSourceName>EM-10-1005B</AlarmSourceName>
    <AlarmSourceDescription>CDU Feed Pump Motor</AlarmSourceDescription>
    <Attribute>HI_ALM</Attribute>
    <Enable>False</Enable>
    <Priority>LOG</Priority>
    <LimitValue>150</LimitValue>
    <Hysteresis>2</Hysteresis>
    <OnDelay>0</OnDelay>
    <OffDelay>0</OffDelay>
    <Path>FIRE_AND_GAS/FG_SYSTEM/EM-10-1005B/HI_ALM</Path>
    <Type>Analog</Type>
    <FunctionalClassificationName>Not classified</FunctionalClassificationName>
  </Alarm>
  <Alarm>
    <AlarmSourceName>FGS-DET-001</AlarmSourceName>
    <AlarmSourceDescription>Gas Detector Area A</AlarmSourceDescription>
    <Attribute>HI_ALM</Attribute>
    <Enable>True</Enable>
    <Priority>WARNING_FG</Priority>
    <LimitValue>25</LimitValue>
    <Hysteresis>5</Hysteresis>
    <OnDelay>0</OnDelay>
    <OffDelay>0</OffDelay>
    <Path>FIRE_AND_GAS/FG_SYSTEM/FGS-DET-001/HI_ALM</Path>
    <Type>Analog</Type>
    <FunctionalClassificationName>Safety</FunctionalClassificationName>
  </Alarm>
</SAMAlarmsReport>'''
