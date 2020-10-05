describe('Manage Plant Test', () => {

  let plantID
  let userToAdd = "tomato150"

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
    }).as('getPlants');
    cy.route({
      method: 'POST',
      url: '/remove_plant_link'
    }).as('removeUser');
    cy.route({
      method: 'POST',
      url: '/add_plant_link'
    }).as('addUser');


  });
  it('Tests user can be added to and removed from plant', () => {
    cy.visit("/login")
    cy.get('#basic_username').type("mateo")
    cy.get('#basic_password').type("123helloo")
    cy.get('[data-cy=test]').click()

    cy.wait('@appLogin').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      expect(xhr.responseBody.access_token).to.exist
    })
    //WHICH PLANT TO PERFORM TEST ON, MATTERS, MUST BE OWNED BY ACCOUNT
    const plantToSelect = 5
    cy.wait('@getPlants').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      plantID = xhr.responseBody[plantToSelect].plant_id
      const plantName = xhr.responseBody[plantToSelect].plant_name

      //const userToAdd = "tomato150"
      cy.wrap({ 'userToAdd': userToAdd }).as('userToAdd')
      cy.wrap({ 'plantID': plantID }).as('plantID')

      cy.get(':nth-child(' + (plantToSelect + 1) + ') > .ant-card-head > .ant-card-head-wrapper > .ant-card-extra > a').click()
      //cy.url().should('include', '/plant/' + plantID)
      //cy.get('[data-cy="plant_name"').should('contain', plantName)
      //expect(cy.url()).to.eq(Cypress.config().baseUrl + '/plant/' + plantID)
      cy.get('[data-cy="add_user_button"]').click()
      cy.get('[data-cy="add_user_input"]').type(userToAdd)
      cy.get('[data-cy="add_user_confirm"]').click()
      cy.wait('@addUser').then(xhr => {
        cy.get('[data-cy="user_listed_' + userToAdd + '"]').should('have.text', userToAdd)
        cy.get('[data-cy="remove_user_' + userToAdd + '"]').click()
        cy.get('[data-cy="user_listed_' + userToAdd + '"]').should('not.exist');

      })
    })

  })
})
