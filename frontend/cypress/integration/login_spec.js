
describe('Login Test', () => {
  beforeEach(() => {
    Cypress.config('baseUrl', 'http://localhost:3000');
    cy.server();
    cy.route({
      method: 'POST',
      url: '/login'
    }).as('appLogin');
  });
  it('Tests Incorrect Username/Password', () => {
    cy.visit("/login")
    cy.get('#basic_username').type("test_incorrect123")
    cy.get('#basic_password').type("blah")
    cy.get('[data-cy=test]').click()

    cy.wait('@appLogin').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      expect(xhr.responseBody.errors[0].message).to.eq('username or password is incorrect');
    })
  })
  it('Tests Correct Username/Password', () => {
    cy.visit("/login")
    cy.get('#basic_username').type("mateo")
    cy.get('#basic_password').type("123helloo")
    cy.get('[data-cy=test]').click()

    cy.wait('@appLogin').then(xhr => {
      cy.log(xhr.responseBody);
      cy.log(xhr.requestBody);
      expect(xhr.responseBody.access_token).to.exist
      //expect(xhr.responseBody.errors[0].message).to.eq('username or password is incorrect');
    })
  })
})