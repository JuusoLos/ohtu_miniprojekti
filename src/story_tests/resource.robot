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
Reset Database
    Go To    ${RESET_URL}

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

    Go To    ${HOME_URL}/citations/new
    Click    css=input[id="article-form"]
    Fill Text    css=input[id="article-citation_key"]    ${citation_key}
    Fill Text    css=input[id="article-author"]    Testikirjoittaja
    Fill Text    css=input[id="article-title"]    Testiartikkeli
    Fill Text    css=input[id="article-journal"]    Testijulkaisu
    Fill Text    css=input[id="article-year"]    2026
    Click    css=button[id="article-submit"]

    RETURN    ${citation_key}

Create Book
    [Arguments]    ${citation_key}=${EMPTY}
    IF    '${citation_key}' == '${EMPTY}'
        ${random}=    Evaluate    __import__('uuid').uuid4().hex[:10]
        ${citation_key}=    Set Variable    TEST${random}
    END

    Go To    ${HOME_URL}/citations/new
    Click    css=input[id="book-form"]
    Fill Text    css=input[id="book-citation_key"]    ${citation_key}
    Fill Text    css=input[id="book-author"]    Testikirjoittaja
    Fill Text    css=input[id="book-title"]    Testikirja
    Fill Text    css=input[id="book-publisher"]    Testijulkaisija
    Fill Text    css=input[id="book-year"]    2026
    Fill Text    css=input[id="book-pages"]    1-12
    Fill Text    css=input[id="book-edition"]    1
    Click    css=button[id="book-submit"]

    RETURN    ${citation_key}

Create Conference Article
    [Arguments]    ${citation_key}=${EMPTY}
    IF    '${citation_key}' == '${EMPTY}'
        ${random}=    Evaluate    __import__('uuid').uuid4().hex[:10]
        ${citation_key}=    Set Variable    TEST${random}
    END

    Go To    ${HOME_URL}/citations/new
    Click    css=input[id="conference-article-form"]
    Fill Text     css=input[id="conf-citation_key"]    ${citation_key}
    Fill Text     css=input[id="conf-author"]    Testikirjoittaja
    Fill Text     css=input[id="conf-title"]    Testijulkaisu
    Fill Text     css=input[id="conf-pages"]    1-23
    Fill Text     css=input[id="conf-conference_name"]    Testikonferenssi
    Fill Text     css=input[id="conf-city"]   Testikaupunki
    Fill Text     css=input[id="conf-year"]    2026
    Click    css=button[id="conf-submit"]

    RETURN    ${citation_key}
