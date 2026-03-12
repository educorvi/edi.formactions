# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.formactions -t test_annotation_storage_handler.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.formactions.testing.EDI_FORMACTIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/formactions/tests/robot/test_annotation_storage_handler.robot
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

Scenario: As a site administrator I can add a Annotation Storage Handler
  Given a logged-in site administrator
    and an add Button form
   When I type 'My Annotation Storage Handler' into the title field
    and I submit the form
   Then a Annotation Storage Handler with the title 'My Annotation Storage Handler' has been created

Scenario: As a site administrator I can view a Annotation Storage Handler
  Given a logged-in site administrator
    and a Annotation Storage Handler 'My Annotation Storage Handler'
   When I go to the Annotation Storage Handler view
   Then I can see the Annotation Storage Handler title 'My Annotation Storage Handler'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Button form
  Go To  ${PLONE_URL}/++add++Button

a Annotation Storage Handler 'My Annotation Storage Handler'
  Create content  type=Button  id=my-annotation_storage_handler  title=My Annotation Storage Handler

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Annotation Storage Handler view
  Go To  ${PLONE_URL}/my-annotation_storage_handler
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Annotation Storage Handler with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Annotation Storage Handler title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
