# Created by Dovadzhyan.VA at 15.05.2023
Feature: Search and selection of a product on market.yandex.ru
As a user of market.yandex.ru
I want to search and select a product within a specific price range and screen size


  Scenario: Visit market.yandex.ru
    Given the browser is open and maximized
    When the user navigates to the "market.yandex.ru" page
    Then the page should load successfully

  Scenario: Select Smartphones subcategory
    When the user clicks on "Catalog" and select "Smartphones" subcategory
    Then the "Smartphones page" should be displayed

  Scenario: Set search parameters (Price, Screen Size)
    When the user sets "Max price parameter" to "20000" Rubles and "Screen Size parameter" from "3" inches
    Then the search parameters should be updated

  Scenario: Select at least 5 brands
    When the user selects at least 5 Brands from the list
    Then at least 5 Brands are selected in the search parameters

#Отсутствует кнопка показать результат (js подгружает после каждого изменения фильтра)
  #Scenario: Show search results
    #When the user clicks on the "Show" button
    #Then the corresponding search results should be displayed

  Scenario: Count number of smartphones on one page
    When the user counts the number of smartphones on one page
    Then the count in Search result should be more than 0

  Scenario: Remember the last one in the list
    When the user is at the End of the page
    Then the user should remember the last smartphone in Search result

  Scenario: Change sorting option
    When the user changes the Sorting option to a different one (Price, Rating, Discount)
    Then the search results should be updated accordingly

  Scenario: Find and click on the name of the remembered smartphone
    When the user looking for the Remembered smartphone in Search result and click on it
    Then the user should see the page and Rating of the selected smartphone

  Scenario: Close the browser
    When the user closes the browser
    Then the browser should close successfully