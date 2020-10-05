describe('View Plant Test', () => {
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
  });
  it('Tests correct plant is viewed upon selection, and that name is correct', () => {
    cy.visit("/login")
    cy.get('#basic_username').type("mateo")
    cy.get('#basic_password').type("123helloo")
    cy.get('[data-cy=test]').click()

    cy.wait('@appLogin').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      expect(xhr.responseBody.access_token).to.exist
    })
    const plantToSelect = 0
    cy.wait('@getPlants').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      const plantID = xhr.responseBody[plantToSelect].plant_id
      const plantName = xhr.responseBody[plantToSelect].plant_name
      cy.get(':nth-child(' + (plantToSelect + 1) + ') > .ant-card-head > .ant-card-head-wrapper > .ant-card-extra > a').click()
      cy.url().should('include', '/plant/' + plantID)
      cy.get('[data-cy="plant_name"').should('contain', plantName)
      //expect(cy.url()).to.eq(Cypress.config().baseUrl + '/plant/' + plantID)

    })
    //cy.expect(cy.get(':nth-child(1) > .ant-card-head > .ant-card-head-wrapper > .ant-card-head-title')).to.eq('helllooo')
    //cy.log(plantName)
    // /cy.get(':nth-child(1) > .ant-card-head > .ant-card-head-wrapper > .ant-card-extra > a').click()
    //.ant - layout - header > .ant - typography
  })
})