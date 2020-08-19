import { HomePage, ChartPage, TradingPage, SimulaPage } from '.';
import HomeIcon from '@material-ui/icons/Home';
import BarChartOutlinedIcon from '@material-ui/icons/BarChartOutlined';
import ShoppingBasketIcon from '@material-ui/icons/ShoppingBasket'
import FindInPageIcon from '@material-ui/icons/FindInPage'

const Routes = [
    {
        path: '/',
        sidebarName: 'Home',
        navbarName: 'Home',
        icon: HomeIcon,
        component: HomePage,
    },
    {
        path: '/chart',
        sidebarName: 'Chart',
        navbarName: 'Chart',
        icon: BarChartOutlinedIcon,
        component:ChartPage,
    },
    {
        path: '/trading',
        sidebarName: 'Trading',
        navbarName: 'Trading',
        icon: ShoppingBasketIcon,
        component:  TradingPage,
    },
    {
        path: '/simula',
        sidebarName: 'Simula',
        navbarName: 'Simula',
        icon: FindInPageIcon,
        component:  SimulaPage,
    }
];

export default Routes;
