fem def para;r;DTI
fem def coord;r;DTI
fem def nodes;r;fitted_gas
fem def bases;r;DTI
fem def elements;r;fitted_gas

fem export nodes;fitted_gas as fitted_gas
fem export elements;fitted_gas as fitted_gas

