import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly email = new FormControl('', {
    nonNullable: true,
    validators: [Validators.required, Validators.email],
  });

  protected readonly password = new FormControl('', {
    nonNullable: true,
    validators: [Validators.required, Validators.minLength(6)],
  });

  protected readonly form = new FormGroup({
    email: this.email,
    password: this.password,
  });

  protected readonly isLoading = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  protected register(): void {
    if (!this.form.valid || this.isLoading()) return;

    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.authService.register(this.email.value, this.password.value).subscribe({
      next: () => {
        // Auto login after registration or just redirect to login
        this.authService.login(this.email.value, this.password.value).subscribe({
            next: () => this.router.navigate(['/']),
            error: () => this.router.navigate(['/login'])
        });
      },
      error: (err) => {
        this.isLoading.set(false);
        if (err.status === 400) {
          this.errorMessage.set('El correo ya está registrado.');
        } else {
          this.errorMessage.set('Se produjo un error al registrarse. Inténtalo de nuevo.');
        }
      },
    });
  }
}
