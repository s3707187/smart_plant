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
    cy.route({
      method: 'GET',
      url: '/get_plant_records?plant_id=37'
    }).as('getPlantHistory')
  });
  it('Tests updating of first and last names', () => {
    cy.request('POST', `http://localhost:8080/login`, { username: "mateo", password: "123helloo" }).then(xhr => {
      cy.log(xhr)
      setAccessToken(xhr.body.access_token)
    });
    cy.visit("/plant/37")
    cy.wait('@getPlantHistory').then(xhr => {

      cy.log(xhr)
      cy.expect(xhr.response.body.length).to.be.greaterThan(48)


    })
  })
})