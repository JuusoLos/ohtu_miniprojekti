*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Artikkelien listauksen näyttäminen
    ${citation_key}=    Create Article

    Go To    ${HOME_URL}

    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    ${citation_key}
    Should Contain    ${page_text}    Testiartikkeli