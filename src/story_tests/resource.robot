*** Settings ***
Library  Browser

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Create Article
    [Arguments]    ${citation_key}=${EMPTY}
    IF    '${citation_key}' == '${EMPTY}'
        ${random}=    Evaluate    __import__('uuid').uuid4().hex[:10]
        ${citation_key}=    Set Variable    TEST${random}
    END

    Go To    ${HOME_URL}/articles/new
    Fill Text    css=input[name="citation_key"]    ${citation_key}
    Fill Text    css=input[name="author"]    Testikirjoittaja
    Fill Text    css=input[name="title"]    Testiartikkeli
    Fill Text    css=input[name="journal"]    Testijulkaisu
    Fill Text    css=input[name="year"]    2026
    Click    css=button[type="submit"]

    RETURN    ${citation_key}
