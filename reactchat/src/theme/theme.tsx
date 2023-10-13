import {createTheme, responsiveFontSizes} from "@mui/material";

declare module "@mui/material/styles" {
    interface Theme {
        primaryDraw: {
            width: number;
            closed: number;
        };
        primaryAppBar: {
            height: number;
        };
    }
    interface ThemeOptions {
        primaryDraw: {
            width: number;
            closed: number;
        };
        primaryAppBar: {
            height: number;
        };
    }
}

export const createMuiTheme = () => {
    let theme = createTheme({

        typography: {
            fontFamily: ['IBM Plex Sans', "sans-serif"].join(","),
        },
        primaryDraw: {
            width: 240,
            closed: 70
        },
        primaryAppBar: {
            height: 50,
        },

        components: {
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                }
            }
        }
    });
    theme = responsiveFontSizes(theme);
    return theme;
};

export default createMuiTheme;