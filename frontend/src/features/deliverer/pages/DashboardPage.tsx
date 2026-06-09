import Button from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import Loading from '../../../shared/components/Loading'
import type { Delivery, Deliverer, DelivererSession } from '../types'
import ActionButtons from '../components/ActionButtons'
import DeliveryCard from '../components/DeliveryCard'
import StatusBadge from '../components/StatusBadge'

type DashboardPageProps = {
  session: DelivererSession
  region: string
  loading: boolean
  refreshedAt?: string | null
  deliveries: Delivery[]
  deliverers: Deliverer[]
  onRefresh: () => void
  onAccept: (deliveryId: string) => void
  onAssign: (deliveryId: string, delivererId?: string) => void
  onStatusChange: (status: Deliverer['status']) => void
}

function DashboardPage({
  session,
  region,
  loading,
  refreshedAt,
  deliveries,
  deliverers,
  onRefresh,
  onAccept,
  onAssign,
  onStatusChange,
}: DashboardPageProps) {
  const availableDeliveries = deliveries.filter((delivery) => delivery.status === 'WAITING' || delivery.status === 'ASSIGNED')
  const activeDeliveries = deliveries.filter((delivery) => delivery.status === 'IN_DELIVERY' || delivery.status === 'PICKED_UP')
  const availableDeliverers = deliverers.filter((deliverer) => deliverer.status === 'AVAILABLE')
  const busyDeliverers = deliverers.filter((deliverer) => deliverer.status === 'BUSY' || deliverer.status === 'OCCUPIED')
  const completedDeliveries = deliveries.filter((delivery) => delivery.status === 'DELIVERED')
  const freshnessLabel = refreshedAt ? `Atualizado às ${new Date(refreshedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : 'Aguardando atualização'

  return (
    <section className="grid">
      <div className="metric-grid">
        <Card className="metric-card">
          <p className="metric-card__label">Sessão ativa</p>
          <strong>{session.name}</strong>
          <p>{session.region}</p>
        </Card>
        <Card className="metric-card">
          <p className="metric-card__label">Disponíveis</p>
          <strong>{availableDeliveries.length}</strong>
          <p>Entregas prontas para agir</p>
        </Card>
        <Card className="metric-card">
          <p className="metric-card__label">Em rota</p>
          <strong>{activeDeliveries.length}</strong>
          <p>{completedDeliveries.length} concluídas na lista</p>
        </Card>
        <Card className="metric-card">
          <p className="metric-card__label">Entregadores livres</p>
          <strong>{availableDeliverers.length}</strong>
          <p>{busyDeliverers.length} ocupados</p>
        </Card>
      </div>

      <Card>
        <div className="section-head">
          <div>
            <h2>Disponíveis agora</h2>
            <p>Entregas prontas para atribuição ou aceitação.</p>
          </div>
          <div className="section-head__meta">
            <span className="status-chip status-chip--soft">{freshnessLabel}</span>
            <Button variant="ghost" onClick={onRefresh}>Atualizar</Button>
          </div>
        </div>
        {loading && <Loading />}
        {!loading && availableDeliveries.length === 0 && <EmptyState message="Nenhuma entrega disponível para esta região." />}
        <div className="stack">
          {availableDeliveries.map((delivery) => (
            <DeliveryCard
              key={delivery.orderId}
              delivery={delivery}
              actions={{
                onAccept: () => onAccept(delivery.orderId),
                onAssign: () => onAssign(delivery.orderId, session.id),
              }}
            />
          ))}
        </div>
      </Card>

      <Card>
        <div className="section-head">
          <div>
            <h2>Disponibilidade</h2>
            <p>Controle simples de presença e carga operacional.</p>
          </div>
        </div>
        <div className="actions actions--stacked">
          <Button onClick={() => onStatusChange('AVAILABLE')}>AVAILABLE</Button>
          <Button variant="secondary" onClick={() => onStatusChange('BUSY')}>BUSY</Button>
          <Button variant="ghost" onClick={() => onStatusChange('OFFLINE')}>OFFLINE</Button>
        </div>
        <div className="section-head section-head--spaced">
          <div>
            <h2>Entregadores na região</h2>
            <p>{region}</p>
          </div>
        </div>
        <div className="stack">
          {deliverers.map((deliverer) => (
            <Card key={deliverer.id} className="card--subtle">
              <div className="row row--space">
                <div>
                  <strong>{deliverer.name}</strong>
                  <p>{deliverer.phone}</p>
                </div>
                <StatusBadge status={deliverer.status} />
              </div>
            </Card>
          ))}
        </div>
      </Card>
    </section>
  )
}

export default DashboardPage
