#!/usr/bin/env python3

nN  = [ 1, 2, 3 ]
nXC = [ 16, 32, 64, 128, 256, 512 ]

grid = [ 0, 1 ]
fc   = [ 0, 1 ]

for g in grid:
    if ( g == 0 ) : sg = 'Single'
    if ( g == 1 ) : sg = 'Multi'
    for f in fc:
        if ( f == 0 ) : sf = '_FCF'
        if ( f == 1 ) : sf = '_FCT'
        if ( g == 0 ) : sf = ''
        if ( ( g == 0 ) & ( f == 1 ) ) : continue
        for nn in nN:
            for nxc in nXC:

                #if ( ( g == 1 ) & ( nxc != 32 ) ) : continue
                sn   = str( nn  ).zfill( 2 )
                snxc = str( nxc ).zfill( 4 )

                fname = 'Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.inputs' \
                          .format( sn, snxc, sg, sf )

                filename = \
'''##### Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.inputs #####

# For all LOGICAL types, use 0 for .FALSE. and 1 for .TRUE.
# For all REAL types, use "e" and not "d", i.e. 1.0e3

thornado.ProgramName = "Advection1D"
thornado.AdvectionProfile = "SineWaveX1"

thornado.nNodes  = {4:}
thornado.t_end   = 1.0e1
thornado.iCycleD = 1
thornado.dt_wrt  = 1.1e+1
thornado.dt_chk  = 1.1e+1

thornado.PlotFileNameRoot        = "Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.plt"
thornado.CheckpointFileNameRoot  = "Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.chk"
thornado.TallyFileNameRoot_Euler = "Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.Tally"
thornado.SuppressTally_Euler     = 1

thornado.bcX         = 01 01 01
geometry.is_periodic = 1 1 1  # Periodic BCs: 0 (no), 1 (yes)

geometry.coord_sys = 0           # CARTESIAN
geometry.prob_lo   = 0.0 0.0 0.0 # Lower domain size
geometry.prob_hi   = 1.0 1.0 1.0 # Upper domain size

thornado.swX                = 01 00 00
amr.n_cell                  = {5:} 01 01 # Number of cells in each dimension
#amr.max_grid_size_x         = 8
#amr.blocking_factor_x       = 4
amr.max_level               = {6:}
amr.UseAMR                  = 0
amr.UseFluxCorrection_Euler = {7:}
amr.TagCriteria             = 0.4 0.2
amr.n_error_buf             = 0
amr.ref_ratio               = 2
amr.UseTiling               = 0

SL.UseSlopeLimiter_Euler           = 0
SL.BetaTVD_Euler                   = 1.75
SL.BetaTVB_Euler                   = 0.0
SL.SlopeTolerance_Euler            = 1.0e-6
SL.UseCharacteristicLimiting_Euler = 1
SL.UseTroubledCellIndicator_Euler  = 1
SL.LimiterThresholdParameter_Euler = 0.03
SL.UseConservativeCorrection       = 1

PL.UsePositivityLimiter_Euler = 0
PL.Min_1_Euler                = 1.0e-13
PL.Min_2_Euler                = 1.0e-13

EoS.EquationOfState = "IDEAL"
EoS.Gamma_IDEAL     = 1.3333333333333333

# Time-Stepping parameters
TS.nStages = {4:}
TS.CFL     = 0.5
'''.format( sn, snxc, sg, sf, nn, nxc, 2*g, f )

                fl = open( fname, 'w' )
                fl.write( filename )
                fl.close()
