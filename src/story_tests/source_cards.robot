*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Tallennetut lahteet nakyvat pelkistettyina kortteina
    ${key1}=    Create Article
    ${key2}=    Create Article

    Go To    ${HOME_URL}
    ${count}=    Get Element Count    css=.source-card
    Should Be Equal As Integers    ${count}    2
    ${card_text}=    Get Text    css=.source-card:nth-child(1)
    Should Contain    ${card_text}    Testiartikkeli
    Should Contain    ${card_text}    Testikirjoittaja
    Should Contain    ${card_text}    2026
    Should Not Contain    ${card_text}    ${key1}
    Should Not Contain    ${card_text}    ${key2}
    Should Not Contain    ${card_text}    Otsikko:
    Should Not Contain    ${card_text}    Viiteavain:
    Should Not Contain    ${card_text}    Julkaisu:
    Should Not Contain    ${card_text}    Testijulkaisu
    Click    css=.source-card:nth-child(1) .source-card-link
    Get Text    css=.citation-details    *=    Testijulkaisu
    Get Text    css=.citation-details    *=    Viiteavain:
