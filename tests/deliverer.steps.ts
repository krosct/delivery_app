import { defineFeature, loadFeature } from 'jest-cucumber'

type DelivererStatus = 'AVAILABLE' | 'OCCUPIED' | 'OFFLINE'

type Deliverer = {
  name: string
  phone: string
  region: string
  status: DelivererStatus
}

const feature = loadFeature('./tests/deliverer.feature')

class DelivererStore {
  private deliverers: Deliverer[] = []

  clear() {
    this.deliverers = []
  }

  create(deliverer: Omit<Deliverer, 'status'>, status: DelivererStatus = 'AVAILABLE'): Deliverer {
    const created: Deliverer = { ...deliverer, status }
    this.deliverers.push(created)
    return created
  }

  count() {
    return this.deliverers.length
  }
}

defineFeature(feature, (test) => {
  let store: DelivererStore
  let response: Deliverer | undefined

  beforeEach(() => {
    store = new DelivererStore()
    response = undefined
  })

  test('cadastrar entregador com sucesso', ({ given, when, then }) => {
    given('nenhum entregador existe', () => {
      store.clear()
    })

    when(/^eu cadastro um entregador com nome "([^"]+)" telefone "([^"]+)" regiao "([^"]+)"$/, (name: string, phone: string, region: string) => {
      response = store.create({ name, phone, region })
    })

    then(/^o entregador "([^"]+)" deve ficar com status "([^"]+)"$/, (name: string, status: DelivererStatus) => {
      expect(response?.name).toBe(name)
      expect(response?.status).toBe(status)
      expect(store.count()).toBe(1)
    })
  })
})