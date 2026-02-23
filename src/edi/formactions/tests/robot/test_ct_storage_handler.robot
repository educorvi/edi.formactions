# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_storage_handler.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_storage_handler.robot
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

Scenario: As a site administrator I can add a Storage Handler
  Given a logged-in site administrator
    and an add Button Handler form
   When I type 'My Storage Handler' into the title field
    and I submit the form
   Then a Storage Handler with the title 'My Storage Handler' has been created

Scenario: As a site administrator I can view a Storage Handler
  Given a logged-in site administrator
    and a Storage Handler 'My Storage Handler'
   When I go to the Storage Handler view
   Then I can see the Storage Handler title 'My Storage Handler'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button Handler form
  Go To  ${PLONE_URL}/++add++Button Handler

a Storage Handler 'My Storage Handler'
  Create content  type=Button Handler  id=my-storage_handler  title=My Storage Handler

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Storage Handler view
  Go To  ${PLONE_URL}/my-storage_handler
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Storage Handler with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Storage Handler title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
