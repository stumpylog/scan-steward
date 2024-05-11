import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { ApiModule } from './api/api.module';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), importProvidersFrom(ApiModule)],
};
