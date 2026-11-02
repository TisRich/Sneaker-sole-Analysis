clc;
clear;
close all;

%STL files
exam = {'Update_FlatS.STL'};
names = {'Flat Sole'};

% exam = {'Curved.STL'};
% names = {'Curved Sole'};


    % Create static structural model
    model = createpde('structural', 'static-solid');

    % Import geometry
    importGeometry(model, exam{1});

    % Check original coordinates in cm
    xyz = model.Geometry.Vertices;
    dimensions_cm = max(xyz,[],1) - min(xyz,[],1);

    fprintf('\n%s\n', names{1});
    fprintf('Dimensions (cm): X=%.2f, Y=%.2f, Z=%.2f\n', ...
        dimensions_cm(1), dimensions_cm(2), dimensions_cm(3));

    fprintf('Number of faces: %d\n', ...
        model.Geometry.NumFaces);

    % Show geometry face numbers
    figure;
    pdegplot(model, ...
        'FaceLabels', 'on', ...
        'FaceAlpha', 0.4);

    axis equal;
    view(3);
    title([names{1}, ' - Face Identification']);

