import { DelivererView } from '../support/views/delivererView'

describe('GUI de entregadores', () => {
  const cases = [
    { name: 'Ana', phone: '11999999999', region: 'Zona Sul', id: '1' },
    { name: 'Bruno', phone: '11888888888', region: 'Centro', id: '2' },
  ]

  cases.forEach((deliverer) => {
    it(`cadastra ${deliverer.name} e atualiza a lista`, () => {
      const view = new DelivererView()

      view.stubList([{ ...deliverer, status: 'AVAILABLE' }])
      view.stubCreate({ ...deliverer, status: 'AVAILABLE' })
      view.visit()

      view.fillForm(deliverer)
      view.submit()
      view.shouldSeeDeliverer(deliverer.name)
    })
  })
})