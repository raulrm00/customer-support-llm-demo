import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, timeout } from 'rxjs';

import { environment } from '../../environments/environment';
import { PredictionRequest, PredictionResponse } from '../models/prediction.model';

@Injectable({
  providedIn: 'root',
})
export class PredictionApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = environment.apiBaseUrl;

  predict(request: PredictionRequest): Observable<PredictionResponse> {
    return this.http
      .post<PredictionResponse>(`${this.apiBaseUrl}/predictions`, request)
      .pipe(timeout(10000));
  }
}
