*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Sovelluksessa on varillinen tausta ja keskitetty sisalto
    Go To    ${HOME_URL}
    ${background}=    Evaluate JavaScript    css=body    (element) => getComputedStyle(element).backgroundColor
    Should Not Be Equal    ${background}    rgb(255, 255, 255)
    ${centered}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.abs(element.getBoundingClientRect().left - (window.innerWidth - element.getBoundingClientRect().right)) < 2
    Should Be True    ${centered}

Etusivulla lomakkeella ja tietosivulla on samat sivumarginaalit
    Create Article
    Go To    ${HOME_URL}
    ${front_left}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().left)
    ${front_width}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().width)
    Go To    ${HOME_URL}/citations/new
    ${form_left}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().left)
    ${form_width}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().width)
    Should Be Equal As Integers    ${front_left}    ${form_left}
    Should Be Equal As Integers    ${front_width}    ${form_width}
    Go To    ${HOME_URL}
    Click    css=.source-card-link
    ${detail_left}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().left)
    ${detail_width}=    Evaluate JavaScript    css=main.page-shell    (element) => Math.round(element.getBoundingClientRect().width)
    Should Be Equal As Integers    ${front_left}    ${detail_left}
    Should Be Equal As Integers    ${front_width}    ${detail_width}

Otsikoissa ja teksteissa on yhtenainen fontti
    Go To    ${HOME_URL}
    ${body_font}=    Evaluate JavaScript    css=body    (element) => getComputedStyle(element).fontFamily
    ${heading_font}=    Evaluate JavaScript    css=h1    (element) => getComputedStyle(element).fontFamily
    Should Be Equal    ${body_font}    ${heading_font}

Lomakkeissa ja lahdekorteissa on sama pyoristys
    Create Article
    Go To    ${HOME_URL}
    ${card_radius}=    Evaluate JavaScript    css=.source-card    (element) => getComputedStyle(element).borderRadius
    Go To    ${HOME_URL}/citations/new
    ${form_radius}=    Evaluate JavaScript    css=.reference-form-panel.article-form    (element) => getComputedStyle(element).borderRadius
    Should Be Equal    ${card_radius}    ${form_radius}

Painikkeiden varitys on sama eri sivuilla
    Go To    ${HOME_URL}
    ${front_color}=    Evaluate JavaScript    css=.homepage-actions .button    (element) => getComputedStyle(element).backgroundColor
    Go To    ${HOME_URL}/citations/new
    ${form_color}=    Evaluate JavaScript    css=#article-submit    (element) => getComputedStyle(element).backgroundColor
    Should Be Equal    ${front_color}    ${form_color}

Lahdekortista avautuu yhtenainen tietosivu
    Create Article
    Go To    ${HOME_URL}
    Click    css=.source-card-link
    Get Text    css=h1    ==    Testiartikkeli
    Get Text    css=.citation-details    *=    Testikirjoittaja
    ${count}=    Get Element Count    css=main.page-shell
    Should Be Equal As Integers    ${count}    1

Kirjan painos ja konferenssijulkaisun tekija nakyvat oikein
    Create Book
    Go To    ${HOME_URL}
    Click    css=.source-card-link
    Get Text    css=.citation-details    *=    Painos: 1
    Create Conference Article
    Go To    ${HOME_URL}
    Click    css=.source-card:last-child .source-card-link
    Get Text    css=.citation-details    *=    Tekijä: Testikirjoittaja
