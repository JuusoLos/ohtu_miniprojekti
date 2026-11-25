*** Settings ***
Resource    resource.robot
Test Setup    Reset Database
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser

*** Test Cases ***
Tallennetut lähteet näkyvät erillisinä nimettyinä kortteina
    ${key1}=    Create Article
    ${key2}=    Create Article

    Go To    ${HOME_URL}
    ${count}=    Get Element Count    css=.source-card
    Should Be Equal As Integers    ${count}    2
    ${page_text}=    Get Text    css=.source-card-list
    Should Contain    ${page_text}    ${key1}
    Should Contain    ${page_text}    ${key2}
    Get Text    css=.source-card:nth-child(1)    *=    Otsikko:
    Get Text    css=.source-card:nth-child(1)    *=    Kirjoittaja:
    Get Text    css=.source-card:nth-child(1)    *=    Julkaisu:
    Get Text    css=.source-card:nth-child(1)    *=    Vuosi:
    Get Text    css=.source-card:nth-child(1)    *=    Viiteavain:
