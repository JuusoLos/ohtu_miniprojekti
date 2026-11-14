*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Artikkelin lisääminen ja viiteavaimen yksilöllisyys
    ${random}=    Evaluate    __import__('uuid').uuid4().hex[:10]
    ${citation_key}=    Set Variable    TEST${random}

    Go To    ${HOME_URL}/articles/new

    Fill Text    css=input[name="citation_key"]    ${citation_key}
    Fill Text    css=input[name="author"]    Testikirjoittaja
    Fill Text    css=input[name="title"]    Testiartikkeli
    Fill Text    css=input[name="journal"]    Testijulkaisu
    Fill Text    css=input[name="year"]    2026

    Click    css=button[type="submit"]

    Get Text    css=[role="status"]    ==    Artikkeli tallennettu.

    Go To    ${HOME_URL}/articles/new

    Fill Text    css=input[name="citation_key"]    ${citation_key}
    Fill Text    css=input[name="author"]    Testikirjoittaja
    Fill Text    css=input[name="title"]    Testiartikkeli
    Fill Text    css=input[name="journal"]    Testijulkaisu
    Fill Text    css=input[name="year"]    2026

    Click    css=button[type="submit"]

    Get Text    css=[role="alert"]    ==    Viiteavain on jo käytössä.