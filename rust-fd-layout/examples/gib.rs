#[macro_use]
extern crate serde_derive;

extern crate getopts;
extern crate serde;
extern crate serde_json;
extern crate fd_layout;

use fd_layout::force::{Point, Link, Force};
use fd_layout::link_force::LinkForce;
use fd_layout::group_force::{Group, GroupForce};
// use fd_layout::node_force::{PointForce}
use fd_layout::simulation::start_simulation;
use fd_layout::edge_bundling::edge_bundling;

#[derive(Serialize, Deserialize)]
struct NodeData {
    group: usize,
}

#[derive(Serialize, Deserialize)]
struct LinkData {
    source: usize,
    target: usize,
    value: f32,
}

#[derive(Serialize, Deserialize)]
struct GroupData {
    x: f32,
    y: f32,
    dx: f32,
    dy: f32,
}

#[derive(Serialize, Deserialize)]
struct GraphData {
    nodes: Vec<NodeData>,
    links: Vec<LinkData>,
    groups: Vec<GroupData>,
}

fn main() {
    let args = std::env::args().collect::<Vec<_>>();
    let mut opts = getopts::Options::new();
    opts.reqopt("f", "file", "input filename", "FILENAME");
    let matches = match opts.parse(&args[1..]) {
        Ok(m) => m,
        Err(f) => panic!(f.to_string()),
    };
    let filename = matches.opt_str("f").unwrap();

    let path = std::path::Path::new(&filename);
    let file = std::fs::File::open(&path).unwrap();
    let mut graph: GraphData = serde_json::from_reader(&file).unwrap();

    let scale = 5.;
    for group in graph.groups.iter_mut() {
        group.x += group.dx / 2.;
        group.y += group.dy / 2.;
        group.x *= scale;
        group.y *= scale;
        group.dx *= scale;
        group.dy *= scale;
    }

    let mut points = graph
        .nodes
        .iter()
        .enumerate()
        .map(|(i, _)| {
            let r = (i as usize as f32).sqrt();
            let theta = std::f32::consts::PI * (3. - (5. as f32).sqrt()) * (i as usize as f32);
            let x = r * theta.cos();
            let y = r * theta.sin();
            Point::new(x, y)
        })
        .collect::<Vec<_>>();
    let links = graph
        .links
        .iter()
        .map(|link| {
            let source_group = graph.nodes[link.source].group;
            let target_group = graph.nodes[link.target].group;
            let (length, strength) = if source_group == target_group {
                let dx = graph.groups[source_group].dx;
                let dy = graph.groups[source_group].dy;
                (dx.min(dy) * 0.6, 0.1)
            } else {
                (1.0, 0.)
            };
            Link {
                source: link.source,
                target: link.target,
                length: length,
                strength: strength,
            }
        })
        .collect::<Vec<_>>();
    let groups = graph
        .groups
        .iter()
        .map(|group| Group::new(group.x, group.y, group.dx, group.dy))
        .collect::<Vec<_>>();
    let node_groups = graph
        .nodes
        .iter()
        .map(|node| node.group)
        .collect::<Vec<_>>();
    let group_colors = {
        let n = graph.groups.len();
        (0..n)
            .map(|i| format!("hsl({}, 100%, 50%)", 360 / n * i))
            .collect::<Vec<_>>()
    };
    eprintln!("start");

////////////////////////// memo ////////////////////////////////

    // let mut nodes_in_group = Vec::new();
    // for _group in groups.iter() {
    //     let mut vec: Vec<i32> = Vec::new();
    //     nodes_in_group.push(vec);
    // }
    // let mut number: i32 = 0;
    // for _index in graph.nodes.iter(){
    //     // eprintln!("{}", _index.group);
    //     nodes_in_group[_index.group].push( number);
    //     number += 1;
    // }
    // for i in nodes_in_group{
    //     if i.len() != 0 {
    //         for j in 0..(i.len() - 1 ) {
    //             for k in 0..(i.len() - j - 1){
    //                 eprintln!("{}, {}", i[j], i[j+k+1]);
    //             }
    //         }
    //     }
    // }



    let forces = {
        let mut forces: Vec<Box<Force>> = Vec::new();
        forces.push(Box::new(LinkForce::new(&links)));
        let mut group_force = GroupForce::new(groups, node_groups);
        group_force.strength = 0.028;
        forces.push(Box::new(group_force));
        forces
    };
    start_simulation(&mut points, &forces);
    eprintln!("bundling edges");
    let lines = edge_bundling(&points, &links);

    eprintln!("writing result");
    {
        let rect = &graph.groups.last().unwrap();
        let width = rect.dx;
        let height = rect.dy;
        let margin = 10.;
        println!(
            "<svg version=\"1.1\" width=\"{}\" height=\"{}\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">",
            width + margin * 2., height + margin * 2.,
            );
        println!(
            "<g transform=\"translate({},{})scale({})\">",
            margin,
            margin,
            1. / scale,
            );
    }
    for group in graph.groups {
        println!(
            "<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" fill=\"none\" stroke=\"black\" />",
            group.x - group.dx / 2.,
            group.y - group.dy / 2.,
            group.dx,
            group.dy,
        );
    }
    for line in lines.iter() {
        let d = line.points
            .iter()
            .map(|p| format!("{} {}", p.x, p.y))
            .collect::<Vec<_>>()
            .join(" L ");
        println!(
            "<path d=\"M {}\" fill=\"none\" stroke=\"#888\" stroke-width=\"5\" opacity=\"0.2\" />",
            d
        );
    }
    for (point, node) in points.iter().zip(graph.nodes.iter()) {
        println!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"10\" fill=\"{}\" />",
            point.x,
            point.y,
            group_colors[node.group],
        );
    }
    println!("</g>\n</svg>");
}
