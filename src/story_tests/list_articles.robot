*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Artikkelien listauksen näyttäminen
    Go To   ${HOME_URL}
    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    Ei lisättyjä lähteitä.

    ${citation_key}=    Create Article

    Go To    ${HOME_URL}

    ${page_text}=    Get Text    css=.source-card-list
    Should Contain    ${page_text}    Testiartikkeli
    Should Contain    ${page_text}    Testikirjoittaja
    Should Contain    ${page_text}    2026
    Should Not Contain    ${page_text}    ${citation_key}