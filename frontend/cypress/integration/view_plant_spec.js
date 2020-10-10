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
    cy.request('POST', `http://localhost:8080/login`, { username: "mateo", password: "123helloo" }).then(xhr => {
      cy.log(xhr)
      setAccessToken(xhr.body.access_token)
    });
    cy.visit("/")
    //WHICH PLANT TO PERFORM TEST ON, FOR VIEW_PLANT SHOULDN'T MATTER
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