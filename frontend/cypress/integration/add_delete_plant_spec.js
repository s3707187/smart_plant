import { setAccessToken, setRefreshToken } from "../../src/app/token.ts"
Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from
  // failing the test
  return false
})

let plantName = "plant_test_name_DELETE_IF_EXISTS"
describe('Add and Delete Plant Test', () => {
  beforeEach(() => {
    Cypress.config('baseUrl', 'http://localhost:3000');
    cy.server();
    cy.route({
      method: 'POST',
      url: '/login'
    }).as('appLogin');
    cy.route({
      method: 'GET',
      url: '/get_users_plants'
    }).as('getPlants')
    cy.request('POST', `http://localhost:8080/login`, { username: "mateo", password: "123helloo" }).then(xhr => {
      cy.log(xhr)
      setAccessToken(xhr.body.access_token)
    });
  });
  it('Tests plant can be added', () => {
    cy.visit("/")
    cy.wait('@getPlants').then(xhr => {
      cy.get('[data-cy=add_plant_button]').click()
      cy.get('#basic_plant_name').type(plantName)
      cy.get('.ant-select-selector').click()
      cy.get('[data-cy=plant_option]').click()
      cy.get('.ant-modal-footer > .ant-btn-primary').click()
    })
  })
  it('Tests plant can be deleted', () => {
    let plantID;
    cy.wait('@getPlants').then(xhr => {
      cy.log(xhr)
      //A more robust approach would be to check for the specific ID
      const plant_N = xhr.responseBody.length
      plantID = xhr.responseBody[plant_N - 1].plant_id
      cy.get(':nth-child(' + (plant_N) + ') > .ant-card-head > .ant-card-head-wrapper > .ant-card-extra > a').click()

      //Double checks that correct plant is being deleted, so as not to interfere with other data/tests
      cy.url().should('include', '/plant/' + plantID)

      cy.get('[data-cy=plant_settings]').click()
      cy.get('[data-cy=delete_plant_confirm]').click()
      cy.get('.ant-btn-primary').click()

    })
    //Upon reload, checks that newly created plant ID is not present in API response
    cy.wait('@getPlants').then(xhr => {
      cy.log(xhr)
      const idExistsInArray = xhr.responseBody.some(plant => plant.plant_id === plantID)
      cy.log(idExistsInArray)
      cy.expect(idExistsInArray).to.equal(false)
    })
  })
})