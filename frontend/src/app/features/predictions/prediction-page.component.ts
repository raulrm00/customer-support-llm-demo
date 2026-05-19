import {
  ChangeDetectionStrategy,
  Component,
  computed,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { finalize, map, startWith } from 'rxjs';

import { PredictionResponse } from '../../models/prediction.model';
import { PredictionApiService } from '../../services/prediction-api.service';

const MAX_INSTRUCTION_LENGTH = 5000;

const CATEGORY_LABELS: Record<PredictionResponse['prediction'], string> = {
  ORDER: 'Pedido',
  SHIPPING: 'Envio',
  CANCEL: 'Cancelacion',
  INVOICE: 'Factura',
  PAYMENT: 'Pago',
  REFUND: 'Reembolso',
  FEEDBACK: 'Comentarios',
  CONTACT: 'Contacto',
  ACCOUNT: 'Cuenta',
  DELIVERY: 'Entrega',
  SUBSCRIPTION: 'Suscripcion',
};

@Component({
  selector: 'app-prediction-page',
  imports: [ReactiveFormsModule],
  templateUrl: './prediction-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PredictionPageComponent {
  private readonly predictionApi = inject(PredictionApiService);

  protected readonly instruction = new FormControl('', {
    nonNullable: true,
    validators: [
      Validators.required,
      Validators.maxLength(MAX_INSTRUCTION_LENGTH),
    ],
  });

  protected readonly form = new FormGroup({
    instruction: this.instruction,
  });

  protected readonly isLoading = signal(false);
  protected readonly isFormValid = toSignal(
    this.instruction.statusChanges.pipe(
      startWith(this.instruction.status),
      map(() => this.instruction.valid),
    ),
    { initialValue: false },
  );
  protected readonly result = signal<PredictionResponse | null>(null);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly maxLength = MAX_INSTRUCTION_LENGTH;
  protected readonly categoryLabels = CATEGORY_LABELS;
  protected readonly canSubmit = computed(
    () => this.isFormValid() && !this.isLoading(),
  );

  protected submit(): void {
    const normalizedInstruction = this.instruction.value.trim();
    this.instruction.setValue(normalizedInstruction, { emitEvent: false });
    this.instruction.markAsTouched();
    this.errorMessage.set(null);

    if (!this.instruction.valid || this.isLoading()) {
      return;
    }

    this.isLoading.set(true);
    this.result.set(null);

    this.predictionApi
      .predict({ instruction: normalizedInstruction })
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (response) => this.result.set(response),
        error: () =>
          this.errorMessage.set(
            'No se pudo obtener la prediccion. Intentalo de nuevo.',
          ),
      });
  }

  protected confidencePercent(confidence: number | null): string {
    if (confidence === null) {
      return 'No disponible';
    }

    return `${Math.round(confidence * 100)} %`;
  }
}
