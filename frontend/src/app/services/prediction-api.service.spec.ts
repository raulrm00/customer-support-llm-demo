import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { PredictionApiService } from './prediction-api.service';

describe('PredictionApiService', () => {
  let service: PredictionApiService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });

    service = TestBed.inject(PredictionApiService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('sends prediction requests to the backend API', () => {
    const payload = { instruction: 'Where is my order?' };

    service.predict(payload).subscribe((response) => {
      expect(response.prediction).toBe('ORDER');
      expect(response.confidence).toBe(0.92);
    });

    const request = httpTesting.expectOne(
      `${environment.apiBaseUrl}/predictions`,
    );
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(payload);
    request.flush({
      prediction: 'ORDER',
      confidence: 0.92,
      model_version: '1.0.0',
      pipeline_version: '1.0.0',
    });
  });
});
