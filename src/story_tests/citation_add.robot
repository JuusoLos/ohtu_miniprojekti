*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Artikkelin lisääminen ja viiteavaimen yksilöllisyys
    ${citation_key}=    Create Article

    Create Article    ${citation_key}
    Sleep    0.1s
    Get Text    css=p[role="alert"]    ==    Viiteavain on jo käytössä.

Kirjan lisääminen ja viiteavaimen yksilöllisyys
    ${citation_key}=    Create Book

    Create Book    ${citation_key}
    Sleep    0.1s
    Get Text    css=p[role="alert"]    ==    Viiteavain on jo käytössä.

Konferenssi julkaisun lisääminen ja viiteavaimen yksilöllisyys
    ${citation_key}=    Create Conference Article

    Create Conference Article    ${citation_key}
    Sleep    0.1s
    Get Text    css=p[role="alert"]    ==    Viiteavain on jo käytössä.   