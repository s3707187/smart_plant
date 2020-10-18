import { setAccessToken, setRefreshToken } from "../../src/app/token.ts"
Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from
  // failing the test
  return false
})
describe('Manage User Account', () => {
  beforeEach(() => {
    Cypress.config('baseUrl', 'http://localhost:3000');
    cy.server();
    cy.route({
      method: 'POST',
      url: '/login'
    }).as('appLogin');
  });
  it('Tests updating of first and last names', () => {
    cy.request('POST', `http://localhost:8080/login`, { username: "mateo", password: "123helloo" }).then(xhr => {
      cy.log(xhr)
      setAccessToken(xhr.body.access_token)
    });
    cy.visit("/profile")
    const newFirst = 'MateoTestName'
    const newLast = 'DiazTestName'
    //cy.get('[data-cy=profile_tab]').click()
    cy.get('[data-cy=edit_user_button]').click()
    cy.get('[data-cy=first_name]').type("{selectall}{backspace}" + newFirst)
    cy.get('[data-cy=last_name]').type("{selectall}{backspace}" + newLast)
    cy.get('.ant-modal-footer > .ant-btn-primary').click()
    cy.get('[data-cy=first_name_data]').should("contain", newFirst)
    cy.get('[data-cy=last_name_data]').should("contain", newLast)

    //Teardown
    cy.get('[data-cy=edit_user_button]').click()
    cy.get('[data-cy=first_name]').type("{selectall}{backspace}" + "Mateo")
    cy.get('[data-cy=last_name]').type("{selectall}{backspace}" + "Diaz")
    cy.get('.ant-modal-footer > .ant-btn-primary').click()
    cy.get('[data-cy=first_name_data]').should("contain", "Mateo")
    cy.get('[data-cy=last_name_data]').should("contain", "Diaz")

  })
})