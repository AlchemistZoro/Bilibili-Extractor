<template>
  <div class="sidebar-wrapper">
    <nav
        :class="{sidebar: true, sidebarStatic, sidebarOpened}"
        @mouseenter="sidebarMouseEnter"
        @mouseleave="sidebarMouseLeave"
    >
      <header class="logo">
        <router-link to="/app/dashboard"><span class="primary-word">V2V</span> <span class="secondary-word"> 视频大数据平台</span></router-link>
      </header>
      <h5 class="navTitle first">
        V2V
      </h5>
      <ul class="nav">
        <NavLink
            :activeItem="activeItem"
            header="总览"
            link="/app/dashboard"
            iconName="flaticon-home"
            index="dashboard"
            isHeader
        />
        <!-- <NavLink
            :activeItem="activeItem"
            header="Notifications"
            link="/app/notifications"
            iconName="flaticon-bell"
            index="notifications"
            isHeader
        /> -->
        <!-- <NavLink
            :activeItem="activeItem"
            header="Components"
            link="/app/components"
            iconName="flaticon-network"
            index="components"
            :childrenLinks="[
              { header: 'Charts', link: '/app/components/charts' },
              { header: 'Icons', link: '/app/components/icons' },
              { header: 'Maps', link: '/app/components/maps' },
            ]"
        /> -->
        <NavLink
            :activeItem="activeItem"
            header="视频"
            link="/app/components/charts"
            iconName="flaticon-network"
            index="components"
            isHeader
        />
        <NavLink
            :activeItem="activeItem"
            header="Typography"
            link="/app/typography"
            iconName="flaticon-list"
            index="typography"
            isHeader
        />
                <NavLink
            :activeItem="activeItem"
            header="Tables Basic"
            link="/app/tables"
            iconName="flaticon-equal-1"
            index="tables"
            isHeader
        />
      </ul>
      <h5 class="navTitle">
        TEAMMATES:
      </h5>
      <ul class="sidebarLabels">
        <li>
          <a href="#">
            <i class="fa fa-circle text-danger"/>
            <span class="labelName">
              范之闽
            </span>
          </a>
        </li>
        <li>
          <a href="#">
            <i class="fa fa-circle text-primary"/>
            <span class="labelName">
              傅毓晗
            </span>
          </a>
        </li>
        <li>
          <a href="#">
            <i class="fa fa-circle text-success"/>
            <span class="labelName">
              王之畅
            </span>
          </a>
        </li>
        <li>
          <a href="#">
            <i class="fa fa-circle text-success"/>
            <span class="labelName">
              朱启鹏
            </span>
          </a>
        </li>
        <li>
          <!-- <a href="#">
            <i class="fa fa-circle text-success"/>
            <span class="labelName">
              ..
            </span>
          </a> -->
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
        <li>
        </li>
      </ul>
      <h5 class="navTitle">
        <!-- PROJECTS -->
      </h5>
      <!-- <div class="sidebarAlerts">
        <b-alert
            v-for="alert in alerts"
            :key="alert.id"
            class="sidebarAlert" variant="transparent"
            show dismissible
        >
          <span>{{alert.title}}</span><br/>
          <b-progress class="sidebarProgress progress-xs mt-1"
                      :variant="alert.color" :value="alert.value" :max="100"/>
          <small>{{alert.footer}}</small>
        </b-alert>
      </div> -->
    </nav>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import isScreen from '@/core/screenHelper';
import NavLink from './NavLink/NavLink';

export default {
  name: 'Sidebar',
  components: { NavLink },
  data() {
    return {
      alerts: [
        {
          id: 0,
          title: 'Sales Report',
          value: 15,
          footer: 'Calculating x-axis bias... 65%',
          color: 'danger',
        },
        {
          id: 1,
          title: 'Personal Responsibility',
          value: 20,
          footer: 'Provide required notes',
          color: 'primary',
        },
      ],
    };
  },
  methods: {
    ...mapActions('layout', ['changeSidebarActive', 'switchSidebar']),
    setActiveByRoute() {
      const paths = this.$route.fullPath.split('/');
      paths.pop();
      this.changeSidebarActive(paths.join('/'));
    },
    sidebarMouseEnter() {
      if (!this.sidebarStatic && (isScreen('lg') || isScreen('xl'))) {
        this.switchSidebar(false);
        this.setActiveByRoute();
      }
    },
    sidebarMouseLeave() {
      if (!this.sidebarStatic && (isScreen('lg') || isScreen('xl'))) {
        this.switchSidebar(true);
        this.changeSidebarActive(null);
      }
    },
  },
  created() {
    this.setActiveByRoute();
  },
  computed: {
    ...mapState('layout', {
      sidebarStatic: state => state.sidebarStatic,
      sidebarOpened: state => !state.sidebarClose,
      activeItem: state => state.sidebarActiveElement,
    }),
  },
};
</script>

<!-- Sidebar styles should be scoped -->
<style src="./Sidebar.scss" lang="scss" scoped/>
