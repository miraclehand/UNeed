import React from 'react';
import Loadable from 'react-loadable';

const Loading = () => {
    return <div>Loading...</div>
};

export const HomePage = Loadable({
    loader: () => import('./HomePage'),
    loading: Loading
});

export const ChartPage = Loadable({
    loader: () => import('./ChartPage'),
    loading: Loading
});

export const TradingPage = Loadable({
    loader: () => import('./TradingPage'),
    loading: Loading
});

export const SimulaPage = Loadable({
    loader: () => import('./SimulaPage'),
    loading: Loading
});

export const SignInPage = Loadable({
    loader: () => import('./SignInPage'),
    loading: Loading
});

export const PopupPage = Loadable({
    loader: () => import('./PopupPage'),
    loading: Loading
});
