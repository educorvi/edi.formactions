# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_button_handler.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_button_handler.robot
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

Scenario: As a site administrator I can add a Button Handler
  Given a logged-in site administrator
    and an add Button Handler form
   When I type 'My Button Handler' into the title field
    and I submit the form
   Then a Button Handler with the title 'My Button Handler' has been created

Scenario: As a site administrator I can view a Button Handler
  Given a logged-in site administrator
    and a Button Handler 'My Button Handler'
   When I go to the Button Handler view
   Then I can see the Button Handler title 'My Button Handler'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button Handler form
  Go To  ${PLONE_URL}/++add++Button Handler

a Button Handler 'My Button Handler'
  Create content  type=Button Handler  id=my-button_handler  title=My Button Handler

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Button Handler view
  Go To  ${PLONE_URL}/my-button_handler
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Button Handler with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Button Handler title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
