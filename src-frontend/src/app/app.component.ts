import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NgxBootstrapIconsModule } from 'ngx-bootstrap-icons';
import { SidebarComponent } from './core/sidebar/sidebar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgxBootstrapIconsModule, RouterOutlet, SidebarComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'scansteward';
}
