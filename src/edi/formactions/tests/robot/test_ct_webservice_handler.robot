# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_webservice_handler.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_webservice_handler.robot
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

Scenario: As a site administrator I can add a Webservice Handler
  Given a logged-in site administrator
    and an add Button Handler form
   When I type 'My Webservice Handler' into the title field
    and I submit the form
   Then a Webservice Handler with the title 'My Webservice Handler' has been created

Scenario: As a site administrator I can view a Webservice Handler
  Given a logged-in site administrator
    and a Webservice Handler 'My Webservice Handler'
   When I go to the Webservice Handler view
   Then I can see the Webservice Handler title 'My Webservice Handler'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button Handler form
  Go To  ${PLONE_URL}/++add++Button Handler

a Webservice Handler 'My Webservice Handler'
  Create content  type=Button Handler  id=my-webservice_handler  title=My Webservice Handler

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Webservice Handler view
  Go To  ${PLONE_URL}/my-webservice_handler
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Webservice Handler with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Webservice Handler title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
