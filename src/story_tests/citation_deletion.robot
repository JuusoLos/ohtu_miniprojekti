*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Yhden lähteen poistaminen jättää toisen
    Create Article
    Create Book

    Go To    ${HOME_URL}
    Click    css=.source-card:nth-child(1) input.source-card-checkbox
    Handle Future Dialogs    action=accept
    Click    css=#delete-citations-button

    ${count}=    Get Element Count    css=.source-card
    Should Be Equal As Integers    ${count}    1
    ${remaining_title}=    Get Text    css=.source-card-link
    Should Be Equal    ${remaining_title}    Testikirja

Kahden lähteen poistaminen jättää artikkelin
    Create Article
    Create Book
    Create Conference Article

    Go To    ${HOME_URL}
    Click    css=.source-card:nth-child(2) input.source-card-checkbox
    Click    css=.source-card:nth-child(3) input.source-card-checkbox
    Handle Future Dialogs    action=accept
    Click    css=#delete-citations-button

    ${count}=    Get Element Count    css=.source-card
    Should Be Equal As Integers    ${count}    1
    ${remaining_title}=    Get Text    css=.source-card-link
    Should Be Equal    ${remaining_title}    Testiartikkeli

Kaikkien lähteiden poistaminen tyhjentää listan
    Create Article
    Create Book
    Create Conference Article

    Go To    ${HOME_URL}
    Click    css=#toggle-citation-selection
    Handle Future Dialogs    action=accept
    Click    css=#delete-citations-button

    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    Ei lisättyjä lähteitä.