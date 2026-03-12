# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_button_group.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_button_group.robot
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

Scenario: As a site administrator I can add a Button Group
  Given a logged-in site administrator
    and an add Form form
   When I type 'My Button Group' into the title field
    and I submit the form
   Then a Button Group with the title 'My Button Group' has been created

Scenario: As a site administrator I can view a Button Group
  Given a logged-in site administrator
    and a Button Group 'My Button Group'
   When I go to the Button Group view
   Then I can see the Button Group title 'My Button Group'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Form form
  Go To  ${PLONE_URL}/++add++Form

a Button Group 'My Button Group'
  Create content  type=Form  id=my-button_group  title=My Button Group

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Button Group view
  Go To  ${PLONE_URL}/my-button_group
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Button Group with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Button Group title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
