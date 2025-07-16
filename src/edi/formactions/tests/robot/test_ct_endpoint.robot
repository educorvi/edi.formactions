# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_endpoint.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_endpoint.robot
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

Scenario: As a site administrator I can add a Endpoint
  Given a logged-in site administrator
    and an add Webservice Handler form
   When I type 'My Endpoint' into the title field
    and I submit the form
   Then a Endpoint with the title 'My Endpoint' has been created

Scenario: As a site administrator I can view a Endpoint
  Given a logged-in site administrator
    and a Endpoint 'My Endpoint'
   When I go to the Endpoint view
   Then I can see the Endpoint title 'My Endpoint'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Webservice Handler form
  Go To  ${PLONE_URL}/++add++Webservice Handler

a Endpoint 'My Endpoint'
  Create content  type=Webservice Handler  id=my-endpoint  title=My Endpoint

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Endpoint view
  Go To  ${PLONE_URL}/my-endpoint
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Endpoint with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Endpoint title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
