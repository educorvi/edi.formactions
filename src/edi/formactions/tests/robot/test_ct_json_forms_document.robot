# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_json_forms_document.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_json_forms_document.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a JsonFormsDocument
  Given a logged-in site administrator
    and an add Folder form
   When I type 'My JsonFormsDocument' into the title field
    and I submit the form
   Then a JsonFormsDocument with the title 'My JsonFormsDocument' has been created

Scenario: As a site administrator I can view a JsonFormsDocument
  Given a logged-in site administrator
    and a JsonFormsDocument 'My JsonFormsDocument'
   When I go to the JsonFormsDocument view
   Then I can see the JsonFormsDocument title 'My JsonFormsDocument'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Folder form
  Go To  ${PLONE_URL}/++add++Folder

a JsonFormsDocument 'My JsonFormsDocument'
  Create content  type=Folder  id=my-json_forms_document  title=My JsonFormsDocument

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the JsonFormsDocument view
  Go To  ${PLONE_URL}/my-json_forms_document
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a JsonFormsDocument with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the JsonFormsDocument title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
