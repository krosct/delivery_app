import Card from '../../../shared/components/Card'
import EmptyState from '../../../shared/components/EmptyState'
import type { Delivery, DelivererSession } from '../types'
import ActionButtons from '../components/ActionButtons'

type ActiveDeliveryPageProps = {
  session: DelivererSession
  delivery: Delivery | null
  onAccept: (deliveryId: string) => void
  onPickup: (deliveryId: string) => void
  onDeliver: (deliveryId: string) => void
}

function ActiveDeliveryPage({ session, delivery, onAccept, onPickup, onDeliver }: ActiveDeliveryPageProps) {
  return (
    <section className="grid">
      <Card>
        <div className="section-head">
          <div>
            <h2>Entrega ativa</h2>
            <p>O próximo passo aparece aqui com prioridade máxima.</p>
          </div>
        </div>
        {delivery ? (
          <div className="stack">
            <div className="status-strip">
              <span className="status-chip status-chip--soft">Aceitar</span>
              <span className="status-chip status-chip--soft">Coletar</span>
              <span className="status-chip status-chip--soft">Entregar</span>
            </div>
            <p><strong>Entregador:</strong> {session.name}</p>
            <p><strong>Pedido:</strong> {delivery.orderId}</p>
            <p><strong>Status:</strong> {delivery.status}</p>
            <ActionButtons
              onAccept={() => onAccept(delivery.orderId)}
              onPickup={() => onPickup(delivery.orderId)}
              onDeliver={() => onDeliver(delivery.orderId)}
              acceptDisabled={delivery.status !== 'ASSIGNED'}
              pickupDisabled={delivery.status !== 'IN_DELIVERY'}
              deliverDisabled={delivery.status !== 'PICKED_UP'}
            />
          </div>
        ) : (
          <EmptyState message="Nenhuma entrega ativa no momento." />
        )}
      </Card>
    </section>
  )
}

export default ActiveDeliveryPage
