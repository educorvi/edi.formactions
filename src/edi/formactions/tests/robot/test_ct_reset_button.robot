# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_reset_button.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_reset_button.robot
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

Scenario: As a site administrator I can add a Reset Button
  Given a logged-in site administrator
    and an add Button Handler form
   When I type 'My Reset Button' into the title field
    and I submit the form
   Then a Reset Button with the title 'My Reset Button' has been created

Scenario: As a site administrator I can view a Reset Button
  Given a logged-in site administrator
    and a Reset Button 'My Reset Button'
   When I go to the Reset Button view
   Then I can see the Reset Button title 'My Reset Button'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button Handler form
  Go To  ${PLONE_URL}/++add++Button Handler

a Reset Button 'My Reset Button'
  Create content  type=Button Handler  id=my-reset_button  title=My Reset Button

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Reset Button view
  Go To  ${PLONE_URL}/my-reset_button
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Reset Button with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Reset Button title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
