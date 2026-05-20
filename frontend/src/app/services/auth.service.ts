import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';
import { Token, User } from '../models/auth.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly apiBaseUrl = environment.apiBaseUrl;

  private readonly tokenKey = 'auth_token';

  readonly currentUser = signal<User | null>(null);
  readonly isAuthenticated = signal<boolean>(false);

  constructor() {
    this.checkSession();
  }

  login(email: string, password: string): Observable<Token> {
    return this.http.post<Token>(`${this.apiBaseUrl}/auth/login`, { email, password }).pipe(
      tap((response) => {
        this.setToken(response.access_token);
        this.fetchCurrentUser().subscribe();
      }),
    );
  }

  register(email: string, password: string): Observable<User> {
    return this.http.post<User>(`${this.apiBaseUrl}/auth/register`, {
      email,
      password,
    });
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
    this.isAuthenticated.set(true);
  }

  fetchCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiBaseUrl}/auth/me`).pipe(
      tap((user) => {
        this.currentUser.set(user);
        this.isAuthenticated.set(true);
      }),
    );
  }

  private checkSession(): void {
    const token = this.getToken();
    if (token) {
      this.fetchCurrentUser().subscribe({
        error: () => this.logout(),
      });
    }
  }
}
