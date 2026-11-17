*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Artikkelin lisääminen ja viiteavaimen yksilöllisyys
    ${citation_key}=    Create Article

    Create Article    ${citation_key}

    Get Text    css=[role="alert"]    ==    Viiteavain on jo käytössä.