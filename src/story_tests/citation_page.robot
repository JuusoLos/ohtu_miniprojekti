*** Settings ***
Resource    resource.robot
Test Setup    Reset Database 
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Lähde sivulle pääsee
    Create Article
    Click    css=a[href="/"]
    SLEEP    0.1s  
    Click     role=link[name="Testiartikkeli"]
    ${page_text}=    Get Text    body
    Should Contain    ${page_text}    Testikirjoittaja