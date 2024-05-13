import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { NgxBootstrapIconsModule } from 'ngx-bootstrap-icons';
import { house, images, peopleFill } from 'ngx-bootstrap-icons';

// Select some icons (use an object, not an array)
const icons = {
  house,
  images,
  peopleFill,
};

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    importProvidersFrom(NgxBootstrapIconsModule.pick(icons)) /*importProvidersFrom(ApiModule)*/,
  ],
};
