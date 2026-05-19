import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

import { PredictionApiService } from '../../services/prediction-api.service';
import { PredictionPageComponent } from './prediction-page.component';

describe('PredictionPageComponent', () => {
  let fixture: ComponentFixture<PredictionPageComponent>;
  let predictionApi: { predict: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    predictionApi = { predict: vi.fn() };

    await TestBed.configureTestingModule({
      imports: [PredictionPageComponent],
      providers: [{ provide: PredictionApiService, useValue: predictionApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(PredictionPageComponent);
    fixture.detectChanges();
  });

  it('renders the prediction form', () => {
    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelector('h1')?.textContent).toContain(
      'Clasificador de solicitudes',
    );
    expect(element.querySelector('label')?.textContent).toContain(
      'Solicitud del cliente',
    );
    expect(element.querySelector('textarea')).toBeTruthy();
  });

  it('shows required validation for blank input', () => {
    setInstructionValue('   ');
    submitForm();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain(
      'El texto es obligatorio.',
    );
    expect(predictionApi.predict).not.toHaveBeenCalled();
  });

  it('disables submit while invalid', () => {
    const button = fixture.nativeElement.querySelector(
      'button[type="submit"]',
    ) as HTMLButtonElement;

    expect(button.disabled).toBe(true);
  });

  it('renders a successful API response', () => {
    predictionApi.predict.mockReturnValue(
      of({
        prediction: 'ORDER',
        confidence: 0.92,
        model_version: '1.0.0',
        pipeline_version: '1.0.0',
      }),
    );

    setInstructionValue('Necesito saber donde esta mi pedido');
    submitForm();
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent as string;
    expect(predictionApi.predict).toHaveBeenCalledWith({
      instruction: 'Necesito saber donde esta mi pedido',
    });
    expect(text).toContain('Pedido');
    expect(text).toContain('92 %');
    expect(text).toContain('1.0.0');
  });

  it('renders a safe Spanish error message when the API fails', () => {
    predictionApi.predict.mockReturnValue(
      throwError(() => new Error('network failure')),
    );

    setInstructionValue('No puedo pagar la factura');
    submitForm();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain(
      'No se pudo obtener la prediccion. Intentalo de nuevo.',
    );
  });

  function setInstructionValue(value: string): void {
    const textarea = fixture.nativeElement.querySelector(
      'textarea',
    ) as HTMLTextAreaElement;
    textarea.value = value;
    textarea.dispatchEvent(new Event('input'));
    fixture.detectChanges();
  }

  function submitForm(): void {
    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    form.dispatchEvent(new Event('submit'));
  }
});
