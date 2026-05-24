type DelivererData = {
  name: string
  phone: string
  region: string
}

type DelivererPayload = DelivererData & {
  id: string
  status: 'AVAILABLE' | 'OCCUPIED' | 'OFFLINE'
}

export class DelivererView {
  stubList(deliverers: DelivererPayload[]) {
    cy.intercept('GET', '/api/deliverers/**', { items: deliverers }).as('loadDeliverers')
  }

  stubCreate(deliverer: DelivererPayload) {
    cy.intercept('POST', '/api/deliverers/', (req) => {
      req.reply({
        id: deliverer.id,
        name: req.body.name,
        phone: req.body.phone,
        region: req.body.region,
        status: deliverer.status,
      })
    }).as('createDeliverer')
  }

  visit() {
    cy.visit('/')
    cy.wait('@loadDeliverers')
  }

  fillForm(deliverer: DelivererData) {
    cy.get('[data-cy="register-deliverer"]').within(() => {
      cy.get('[data-cy="deliverer-name"]').clear().type(deliverer.name)
      cy.get('[data-cy="deliverer-phone"]').clear().type(deliverer.phone)
      cy.get('[data-cy="deliverer-region"]').clear().type(deliverer.region)
    })
  }

  submit() {
    cy.get('[data-cy="submit-deliverer"]').click()
    cy.wait('@createDeliverer')
  }

  shouldSeeDeliverer(name: string) {
    cy.contains(name).should('be.visible')
  }
}