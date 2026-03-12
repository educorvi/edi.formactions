# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_file_storage_handler.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_file_storage_handler.robot
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

Scenario: As a site administrator I can add a File Storage Handler
  Given a logged-in site administrator
    and an add Button form
   When I type 'My File Storage Handler' into the title field
    and I submit the form
   Then a File Storage Handler with the title 'My File Storage Handler' has been created

Scenario: As a site administrator I can view a File Storage Handler
  Given a logged-in site administrator
    and a File Storage Handler 'My File Storage Handler'
   When I go to the File Storage Handler view
   Then I can see the File Storage Handler title 'My File Storage Handler'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button form
  Go To  ${PLONE_URL}/++add++Button

a File Storage Handler 'My File Storage Handler'
  Create content  type=Button  id=my-file_storage_handler  title=My File Storage Handler

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the File Storage Handler view
  Go To  ${PLONE_URL}/my-file_storage_handler
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a File Storage Handler with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the File Storage Handler title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
