import { render, screen } from '@testing-library/react'
import LoginPage from '../pages/LoginPage'
import type { DelivererLoginForm } from '../types'

describe('LoginPage', () => {
  it('renders the updated deliverer entry point', () => {
    const form: DelivererLoginForm = {
      name: 'Ana',
      phone: '11999999999',
      region: 'Zona Sul',
    }

    render(<LoginPage form={form} onChange={() => {}} onSubmit={() => {}} />)

    expect(screen.getByText('Seu próximo pedido, sem ruído')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Entrar no painel' })).toBeInTheDocument()
  })
})
