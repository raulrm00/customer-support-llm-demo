import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/predictions/prediction-page.component').then(
        (component) => component.PredictionPageComponent,
      ),
  },
];
