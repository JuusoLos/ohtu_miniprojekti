*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Yhden lähteen poistaminen jättää toisen
    ${article_key}=    Create Article
    ${book_key}=    Create Book

    Go To    ${HOME_URL}
    Click    css=.source-card:nth-child(1) input.source-card-checkbox
    Handle Future Dialogs    action=accept
    Click    css=#delete-citations-button

    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    ${book_key}
    Should Not Contain    ${page_text}    ${article_key}

Kahden lähteen poistaminen jättää artikkelin
    ${article_key}=    Create Article
    ${book_key}=    Create Book
    ${conference_key}=    Create Conference Article

    Go To    ${HOME_URL}
    Click    css=.source-card:nth-child(2) input.source-card-checkbox
    Click    css=.source-card:nth-child(3) input.source-card-checkbox
    Handle Future Dialogs    action=accept
    Click    css=#delete-citations-button

    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    ${article_key}
    Should Not Contain    ${page_text}    ${book_key}
    Should Not Contain    ${page_text}    ${conference_key}

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